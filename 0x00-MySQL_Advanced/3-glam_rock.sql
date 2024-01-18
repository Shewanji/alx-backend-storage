-- SQL script to list Glam rock bands ranked by longevity
SELECT
    band_name,
    IF
        (split IS NULL, 2022, split) - formed AS lifespan
FROM
    metal_bands
WHERE
    style LIKE "%Glam rock%"
ORDER BY
    lifespan DESC;
