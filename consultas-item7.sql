-- 7.1
SELECT departamento, SUM(cantidad * precio) AS monto_total 
FROM vista_operaciones 
GROUP BY departamento 
ORDER BY monto_total DESC LIMIT 8;

-- 7.2
SELECT municipio, SUM(cantidad) AS cantidad_total 
FROM vista_operaciones WHERE UPPER(departamento) LIKE '%ANTIOQUIA%' 
GROUP BY municipio 
ORDER BY cantidad_total DESC LIMIT 15;

-- 7.3
SELECT departamento, SUM(cantidad) AS cantidad_total 
FROM vista_operaciones WHERE UPPER(producto) LIKE '%MANZALOCA%' 
GROUP BY departamento 
ORDER BY cantidad_total DESC LIMIT 5;

-- 7.4
SELECT departamento, municipio, SUM(cantidad * precio) AS monto_total 
FROM vista_operaciones 
GROUP BY departamento, municipio 
ORDER BY monto_total ASC LIMIT 5;

-- 7.5
SELECT region, producto, SUM(cantidad) AS cantidad_total 
FROM vista_operaciones 
GROUP BY region, producto 
ORDER BY cantidad_total DESC;

-- 7.6
SELECT producto, SUM(cantidad * precio) AS monto_total 
FROM vista_operaciones WHERE UPPER(departamento) LIKE '%ANTIOQUIA%' 
GROUP BY producto 
ORDER BY monto_total DESC;

