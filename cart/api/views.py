from rest_framework import generics, status
from rest_framework.response import Response

from cart.models import Cart
from .serializer import CartSerializer, CartDelSerializer
from product.models import Products, variants
from rest_framework.permissions import IsAuthenticated


class ADDCartApiView(generics.GenericAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            product_id = serializer.data['product_id']
            variant_id = serializer.data['variant_id']
            quantity = serializer.data['quantity']

            try:
                product = Products.objects.get(id=product_id)
                variant = variants.objects.get(id=variant_id)
                Cart.objects.create(
                    user_id=user.id,
                    product_id=product.id,
                    variant_id=variant.id,
                    quantity=quantity
                )
                context = {'success': 'add to cart.'}
                return Response(context, status=status.HTTP_201_CREATED)
            except Products.DoesNotExist or variants.DoesNotExist:
                context = {'error': 'Product matching query or variant matching query not exists'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDelApiView(generics.GenericAPIView):
    serializer_class = CartDelSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            product_id = serializer.data['product_id']
            variant_id = serializer.data['variant_id']
            try:
                product = Products.objects.get(id=product_id, user_id=user.id)
                variant = variants.objects.get(id=variant_id, user_id=user.id)
                if product.option_status == 'None':
                    Cart.objects.get(product_id=product.id).delete()
                else:
                    Cart.objects.get(variant_id=variant.id).delete()

                context = {'success': 'remove from cart.'}
                return Response(context, status=status.HTTP_200_OK)
            except Products.DoesNotExist or variants.DoesNotExist:
                context = {'error': 'Product matching query or variant matching query not exists'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get(self, request, *args, **kwarg):
        user = request.user

        try:
            queryset = Cart.objects.filter(user_id=user.id)
            serializer = CartDelSerializer(instance=queryset, many= True).data
            return Response({'product': serializer, })
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
