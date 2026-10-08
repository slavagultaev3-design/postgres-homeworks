-- 1. Название компании заказчика и ФИО сотрудника из Лондона с доставкой United Package
SELECT 
    c.company_name, 
    CONCAT(e.first_name, ' ', e.last_name) AS employee_full_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id
JOIN shippers s ON o.ship_via = s.shipper_id
WHERE c.city = 'London' 
  AND e.city = 'London' 
  AND s.company_name = 'United Package';

-- 2. Продукты (Dairy Products и Condiments), не снятые с продажи, которых < 25 шт.
SELECT 
    p.product_name, 
    p.units_in_stock, 
    s.contact_name, 
    s.phone
FROM products p
JOIN suppliers s ON p.supplier_id = s.supplier_id
JOIN categories cat ON p.category_id = cat.category_id
WHERE p.discontinued = 0  -- или p.discontinued = false, если тип boolean
  AND p.units_in_stock < 25
  AND cat.category_name IN ('Dairy Products', 'Condiments')
ORDER BY p.units_in_stock ASC;

-- 3. Список компаний заказчиков, не сделавших ни одного заказа
SELECT company_name
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id 
    FROM orders 
    WHERE customer_id IS NOT NULL
);

-- 4. Уникальные названия продуктов, которых заказано ровно 10 единиц (через подзапрос)
SELECT product_name
FROM products
WHERE product_id IN (
    SELECT product_id
    FROM order_details
    WHERE quantity = 10
);
