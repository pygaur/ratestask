rate_list_query = """
    SELECT "prices"."day", ROUND(AVG("prices"."price"),2)
        AS "total", COUNT(price) AS "times" FROM "prices"
    INNER JOIN "ports" ON ("prices"."orig_code" =
        "ports"."code")
    INNER JOIN "ports" T4 ON ("prices"."dest_code" =
        T4."code")
    WHERE (("prices"."orig_code" = %s)
                    OR
        ("ports"."parent_slug" = %s))
    AND
        (("prices"."dest_code" = %s
                OR
        (T4."parent_slug" = %s)) 
    AND "prices"."day" BETWEEN %s::date AND %s::date)
    GROUP BY "prices"."day"
        """

port_check_query = """
    select code from ports where code=(%s) or code=(%s) limit 2
"""

price_insert_query = """
    insert into prices (orig_code, dest_code, day, price) values (%s, %s, %s, %s)
"""
