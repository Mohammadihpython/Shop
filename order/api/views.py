from rest_framework import generics, status
from rest_framework.response import Response

from cart.models import Cart
from order.models import Order, ItemOrder

from .serializer import OrderSerializer, ItemOrderSerializer
from product.api.views import PostUserPermission


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            discount = serializer.data.get('discount')
            email = serializer.data.get('email')
            f_name = serializer.data.get('f_name')
            l_name = serializer.data.get('l_name')
            address = serializer.data.get('address')
            cart = Cart.objects.filter(user_id=user.id)
            try:
                total_price = sum(
                    c.product.total_price
                    if c.product.option_status == 'None'
                    else c.variant.total_price
                    for c in cart
                )
                order = Order.objects.create(
                    user_id=user.id,
                    discount=discount,
                    email=email,
                    f_name=f_name,
                    l_name=l_name,
                    address=address,
                    paid=False,
                )
                for c in cart:
                    ItemOrder.objects.create(
                        order_id=order.id,
                        user_id=user.id,
                        product_id=c.product.id,
                        variant_id=c.variant.id,
                        quantity=cart.quantity # type: ignore
                    )

                return Response({'data': 'order create','total price':total_price }, status=status.HTTP_201_CREATED)

            except Cart.DoesNotExist:
                return Response('Cart is empty', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListDestroyApiView(generics.ListAPIView):
    serializer_class = ItemOrderSerializer
    permission_classes = [PostUserPermission]

    def get_queryset(self):
        user = self.request.user
        return ItemOrder.objects.filter(user_id=user.id)


class OrderDeleteApiView(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)
