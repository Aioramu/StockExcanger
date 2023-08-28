from .serializers import *


def bulk_create(stock_data: list):
    serializer = StockSerializer(data=stock_data, many=True)
    if serializer.is_valid():
        queryset = serializer.save()

    else:
        return serializer.errors
    return queryset, serializer.data


def update_many_stocks(validated_data: list):
    bulk_list = []
    for ticket in validated_data:
        instance = Stock.objects.get(ticket=ticket["ticket"])
        instance.name = ticket.get("name", None)
        instance.price = ticket.get("price", None)
        instance.pe = ticket.get("pe", None)
        instance.ps = ticket.get("ps", None)
        instance.pb = ticket.get("pb", None)
        instance.ebitda = ticket.get("ebitda", None)
        instance.env = ticket.get("env", None)
        instance.net_worth = ticket.get("net_worth", None)
        instance.roe = ticket.get("roe", None)
        instance.debt_eq = ticket.get("debt_eq", None)
        instance.roa = ticket.get("roa", None)
        instance.roi = ticket.get("roi", None)
        instance.last_divident = ticket.get("last_divident", None)
        bulk_list.append(instance)
    queryset = Stock.objects.bulk_update(bulk_list, list(validated_data[0].keys()))
    serializer = StockSerializer(queryset, many=True)
    return queryset, serializer.data


def bulk_update(stock_data: list) -> list:
    ticker_ids = [x["ticket"] for x in stock_data]
    queryset = Stock.objects.filter(ticket__in=ticker_ids)
    created_tickets = queryset.values_list("ticket", flat=True)
    create_data = [data for data in stock_data if data["ticket"] not in created_tickets]
    update_data = [data for data in stock_data if data["ticket"] in created_tickets]
    data = []

    if len(update_data) != 0:
        serializer = StockSerializer(data=update_data, many=True)
        if serializer.is_valid():
            data = update_many_stocks(serializer.validated_data)[1]
        else:
            return serializer.errors

    if len(create_data) != 0:
        data += bulk_create(create_data)[1]

    return data
