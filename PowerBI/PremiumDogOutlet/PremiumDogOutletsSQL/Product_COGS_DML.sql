ALTER TABLE `Product` ADD COLUMN `COGS`(19,4) DEFAULT 0.00;

UPDATE Product
SET COGS = ROUND(
    CASE
        /* -------------------------
           DOG FOOD – DRY (60%)
        --------------------------*/
        WHEN Category = 'Dog Food' AND SubCategory = 'Dry Dog Food'
            THEN Price * 0.60

        /* -------------------------
           DOG FOOD – CANNED (65%)
        --------------------------*/
        WHEN Category = 'Dog Food' AND SubCategory = 'Canned Dog Food'
            THEN Price * 0.65

        /* -------------------------
           TOYS – RUBBER (45%)
        --------------------------*/
        WHEN Category = 'Dog Toy' AND Material = 'Rubber'
            THEN Price * 0.45

        /* -------------------------
           TOYS – PLUSH (40%)
        --------------------------*/
        WHEN Category = 'Dog Toy' AND Material = 'Plush'
            THEN Price * 0.40

        /* -------------------------
           TOYS – ROPE (40%)
        --------------------------*/
        WHEN Category = 'Dog Toy' AND Material = 'Rope'
            THEN Price * 0.40

        /* -------------------------
           TOY COMBO PACKS (45%)
           e.g. Rubber/Rope
        --------------------------*/
        WHEN Category = 'Dog Toy' AND Material LIKE '%/%'
            THEN Price * 0.45

        /* SAFETY DEFAULT — if anything is missing */
        ELSE Price * 0.60
    END
, 2);
