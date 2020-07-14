CREATE TABLE "cryptos" ("id" INTEGER PRIMARY KEY IDENTITY, 
                        "symbol" TEXT, 
                        "name" TEXT
                        );
                        
CREATE TABLE "movements"("id" INTEGER PRIMARY KEY IDENTITY UNIQUE, 
                        "date" TEXT, 
                        "time" TEXT, 
                        "from_currency" INTEGER, 
                        "from_quantity" REAL, 
                        "to_currency" INTEGER, 
                        "to_quantity" REAL, 
                        "unit_price" REAL, 
                        FOREIGN KEY("from_currency") REFERENCES "cryptos"("symbol"), 
                        FOREIGN KEY("to_currency") REFERENCES "cryptos"("symbol")
                        );