/******************************
Essential Initial Query
******************************/
USE sakila
;

/******************************
Section 1
******************************/
-- 1a)
SELECT first_name, last_name
FROM actor
;

-- 1b)
SELECT UPPER(CONCAT(first_name,' ',last_name))
AS Actor_Name
FROM actor
;

/******************************
Section 2
******************************/
-- 2a)
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'Joe'
;

-- 2b)
SELECT *
FROM actor
WHERE last_name
LIKE '%GEN%'
;

-- 2c)
SELECT *
FROM actor
WHERE last_name
LIKE '%LI%'
ORDER BY last_name,first_name
;

-- 2d)
SELECT country_id, country
FROM country
WHERE country
IN ('Afghanistan',
    'Bangladesh',
    'China'
);

/******************************
Section 3
******************************/
-- 3a)
ALTER TABLE actor
ADD COLUMN description BLOB
;

-- 3b)
ALTER TABLE actor
DROP COLUMN description
;

/******************************
Section 4
******************************/
-- 4a)
SELECT last_name
    ,COUNT(*) AS occurrences
FROM actor
GROUP BY last_name
;

-- 4b)
SELECT last_name
    ,COUNT(*) AS occurrences
FROM actor
GROUP BY last_name
HAVING occurrences > 1
;

-- 4c)
UPDATE actor
SET first_name = 'HARPO'
WHERE first_name = 'GROUCHO'
    AND last_name = 'WILLIAMS'
;

-- 4d)
UPDATE actor
SET first_name = 'GROUCHO'
WHERE first_name = 'HARPO'
;

/******************************
Section 5
******************************/
-- 5a)
SHOW CREATE TABLE address
;

/* This question was a bit confusing what it was asking,
but this is the query from the link in the instructions.
If you're looking for a way to view the schema, an easier way
I've found would be to left click on the address object on the left
and then view tab 5 labeled 'Info' on sqlyog. This spells out
the full schema for address in great detail.
*/

/******************************
Section 6
******************************/
-- 6a)
SELECT s.first_name
      ,s.last_name
      ,a.address
FROM staff AS s
INNER JOIN address AS a
ON s.address_id = a.address_id
;

-- 6b)
SELECT s.first_name
      ,s.last_name
      ,SUM(p.amount) AS total_amount
FROM staff AS s
INNER JOIN payment AS p
ON s.staff_id = p.staff_id
GROUP BY last_name
;

-- 6c)
SELECT f.title
      ,COUNT(fa.actor_id) AS actor_cnt
FROM film AS f
INNER JOIN film_actor AS fa
ON f.film_id = fa.film_id
GROUP BY f.title
;

-- 6d)
SELECT COUNT(inventory_id) AS 'Hunchback_Impossible_Cnt'
FROM inventory
WHERE film_id = 439

-- 6e)
SELECT c.first_name
      ,c.last_name
      ,SUM(p.amount) AS total_amount
FROM customer AS c
INNER JOIN payment AS p
ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY last_name
;

/******************************
Section 7
******************************/
-- 7a)
SELECT title
FROM film
WHERE title LIKE 'K%'
OR title LIKE 'Q%'
AND language_id = 1
;

-- 7b)
SELECT first_name, last_name
FROM actor
WHERE actor_id IN(
    SELECT actor_id 
    FROM film_actor
    WHERE film_id IN(
        SELECT film_id
        FROM film
        WHERE title = 'ALONE TRIP'
    )
);

-- 7c)
SELECT first_name, last_name, email
FROM customer
WHERE address_id IN(
    SELECT address_id 
    FROM address
    WHERE city_id IN(
        SELECT city_id 
        FROM city
        WHERE country_id IN(
            SELECT country_id
            FROM country
            WHERE country = 'Canada'            
        )        
    )    
);

-- 7d)
SELECT title
FROM film
WHERE film_id IN(
    SELECT film_id
    FROM film_category
    WHERE category_id = 8
);

-- 7e)
SELECT f.title
      ,COUNT(i.film_id) AS cnt
FROM film AS f
INNER JOIN inventory AS i
ON f.film_id = i.film_id
WHERE i.film_id IN(
    SELECT film_id
    FROM inventory
    WHERE inventory_id IN(
	SELECT inventory_id
	FROM rental
    )
)
GROUP BY f.title
ORDER BY cnt DESC
;
/**************************************************
-- 7f)
select * from payment;
select * from rental;
SELECT * FROM inventory;
select * from store;

SELECT s.store_id
      ,SUM(p.amount) AS total_amount
FROM store AS s
INNER JOIN inventory AS i
ON s.store_id = i.store_id
where i.inventory_id in(
    select inventory_id
    from inventory
    where rental_id in(
        select rental_id
        from payment
    )
)
GROUP BY s.store_id
;

-- 7g)
select * from city;
select * from country;
select * from store;
select * from address;
select * from customer;

select country
from country
where country_id in(
	select country_id
	from city
	where city_id in(
		select city_id
		from address
		where address in(
			select a.address
			from store as s
			inner join address as a
			on s.address_id = a.address_id
		)
	)
)
inner join 
*/