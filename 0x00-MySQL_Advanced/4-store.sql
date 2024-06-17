-- script that creates a trigger that dcreases the quantity of an item
create trigger edit
after insert on orders
for each row
update items set items.quantity = items.quantity - new.number where new.item_name = items.name;
