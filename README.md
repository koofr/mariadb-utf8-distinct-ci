# mariadb-utf8-distinct-ci

Case insensitive, distinct Unicode collation for MariaDB

The collation is based on the ideas from MariaDB's blog post.

https://mariadb.com/blog/adding-case-insensitive-distinct-unicode-collation

MariaDB 10 or greater is needed.

# Usage

Move `Index.xml` to `/usr/share/mysql/charsets/Index.xml` and restart your MariaDB server.

# Test

```
SELECT 'c' = 'C' COLLATE utf8_unicode_ci;
SELECT 'c' = 'č' COLLATE utf8_unicode_ci;

SELECT 'c' = 'C' COLLATE utf8_distinct_ci;
SELECT 'c' = 'č' COLLATE utf8_distinct_ci;
```
