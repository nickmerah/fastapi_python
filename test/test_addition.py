import pytest

from apps.test_test import add, subtract, multiply, divide, BankAccount


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(100)


@pytest.mark.parametrize("num1, num2, val", [
    (3, -1, 2), (4, 1, 5), (12, 4, 16)
])
def test_add(num1, num2, val):
    assert add(num1, num2) == val


def test_subtract():
    assert subtract(3, 1) == 2


def test_multiply():
    assert multiply(3, 1) == 3


def test_divide():
    assert divide(9, 3) == 3


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100


def test_withdraw_amount(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50


@pytest.mark.parametrize("deposit, withdraw, val", [
    (200, 100, 100), (50, 10, 40), (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, val):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == val


def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)
