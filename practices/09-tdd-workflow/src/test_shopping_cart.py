from shopping_cart import ShoppingCartImpl, CartItem


class TestShoppingCartAddItem:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_add_a_new_item_to_the_cart(self):
        self.cart.add_item(id="1", name="Apple", price=1000)
        items = self.cart.get_items()
        assert len(items) == 1
        assert items[0] == CartItem(id="1", name="Apple", price=1000, quantity=1)

    def test_should_add_item_with_specified_quantity(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=3)
        items = self.cart.get_items()
        assert items[0].quantity == 3

    def test_should_increase_quantity_when_adding_existing_item(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=2)
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=3)
        items = self.cart.get_items()
        assert len(items) == 1
        assert items[0].quantity == 5

    def test_should_throw_error_for_zero_or_negative_quantity(self):
        import pytest
        with pytest.raises(Exception):
            self.cart.add_item(id="1", name="Apple", price=1000, quantity=0)
        with pytest.raises(Exception):
            self.cart.add_item(id="1", name="Apple", price=1000, quantity=-1)

    def test_should_throw_error_for_negative_price(self):
        import pytest
        with pytest.raises(Exception):
            self.cart.add_item(id="1", name="Apple", price=-100)


class TestShoppingCartRemoveItem:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_remove_an_item_from_the_cart(self):
        self.cart.add_item(id="1", name="Apple", price=1000)
        self.cart.add_item(id="2", name="Banana", price=2000)
        self.cart.remove_item("1")
        items = self.cart.get_items()
        assert len(items) == 1
        assert items[0].id == "2"

    def test_should_throw_error_when_removing_non_existent_item(self):
        import pytest
        with pytest.raises(Exception):
            self.cart.remove_item("non-existent")

    def test_should_handle_removing_from_empty_cart(self):
        import pytest
        with pytest.raises(Exception):
            self.cart.remove_item("1")


class TestShoppingCartGetTotal:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_return_0_for_empty_cart(self):
        assert self.cart.get_total() == 0

    def test_should_calculate_total_correctly(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=2)
        self.cart.add_item(id="2", name="Banana", price=1500, quantity=3)
        assert self.cart.get_total() == 2000 + 4500

    def test_should_update_total_after_removing_item(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=2)
        self.cart.add_item(id="2", name="Banana", price=1500, quantity=1)
        self.cart.remove_item("2")
        assert self.cart.get_total() == 2000


class TestShoppingCartApplyDiscount:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_apply_percentage_discount(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=10)
        discounted = self.cart.apply_discount(10)
        assert discounted == 9000

    def test_should_apply_0_percent_discount(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=5)
        discounted = self.cart.apply_discount(0)
        assert discounted == 5000

    def test_should_apply_100_percent_discount(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=5)
        discounted = self.cart.apply_discount(100)
        assert discounted == 0

    def test_should_throw_error_for_discount_over_100(self):
        import pytest
        self.cart.add_item(id="1", name="Apple", price=1000)
        with pytest.raises(Exception):
            self.cart.apply_discount(101)

    def test_should_throw_error_for_negative_discount(self):
        import pytest
        self.cart.add_item(id="1", name="Apple", price=1000)
        with pytest.raises(Exception):
            self.cart.apply_discount(-10)

    def test_should_return_0_for_empty_cart_regardless_of_discount(self):
        discounted = self.cart.apply_discount(50)
        assert discounted == 0


class TestShoppingCartClearCart:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_remove_all_items(self):
        self.cart.add_item(id="1", name="Apple", price=1000)
        self.cart.add_item(id="2", name="Banana", price=2000)
        self.cart.clear_cart()
        assert len(self.cart.get_items()) == 0
        assert self.cart.get_total() == 0

    def test_should_handle_clearing_empty_cart(self):
        self.cart.clear_cart()
        assert len(self.cart.get_items()) == 0


class TestShoppingCartGetItemCount:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_return_0_for_empty_cart(self):
        assert self.cart.get_item_count() == 0

    def test_should_return_total_quantity_of_all_items(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=3)
        self.cart.add_item(id="2", name="Banana", price=2000, quantity=2)
        assert self.cart.get_item_count() == 5

    def test_should_update_count_after_operations(self):
        self.cart.add_item(id="1", name="Apple", price=1000, quantity=3)
        self.cart.add_item(id="2", name="Banana", price=2000, quantity=2)
        self.cart.remove_item("1")
        assert self.cart.get_item_count() == 2
        self.cart.clear_cart()
        assert self.cart.get_item_count() == 0


class TestShoppingCartImmutability:
    def setup_method(self):
        self.cart = ShoppingCartImpl()

    def test_should_return_a_copy_of_items_not_the_internal_list(self):
        self.cart.add_item(id="1", name="Apple", price=1000)
        items = self.cart.get_items()
        items.append(CartItem(id="2", name="Hack", price=0, quantity=1))
        assert len(self.cart.get_items()) == 1
