from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        category = self.request.query_params.get('category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if category:
            queryset = queryset.filter(category__iexact=category)

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
class ExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period')

        today = timezone.now().date()

        if period == 'weekly':
            start_date = today - timedelta(days=today.weekday())
        elif period == 'monthly':
            start_date = today.replace(day=1)
        else:
            return Response(
                {"error": "Invalid period. Use 'weekly' or 'monthly'."},
                status=400
            )

        total = Expense.objects.filter(
            user=request.user,
            date__range=[start_date, today]
        ).aggregate(total_spent=Sum('amount'))['total_spent'] or 0

        return Response({
            "period": period,
            "total_spent": float(total)
        })    