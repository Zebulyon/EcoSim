#!/bin/bash

function run
{
    echo Currency:  $currency, Trade: $trade, Actor amount: $amountOfActors, Resource amount: $amountOfResources, Min init resources: $min_init_resources, Max init resources: $max_init_resources, Min init productio: $min_init_production, Max init production: $max_init_production, Min init amount to sell: $min_init_amountToSell, Max init amount to sell: $max_init_amountToSell, Min init price divergence: $min_init_priceDivergence, Max init price divergence: $max_init_priceDivergence, Days: $days >> out.txt
    testnum=$[ $testnum + 1 ]
    echo "Running " $testnum
    ./Society.py $currency $trade $converging_value $amountOfActors $amountOfResources $min_init_resources $max_init_resources $min_init_production $max_init_production $min_init_amountToSell $max_init_amountToSell $min_init_priceDivergence $max_init_priceDivergence $days >> out.txt
}
testnum=0
echo "" > out.txt
echo "Tests - Non-converging Medium init resources medium production medium price divergence 40 days" >> out.txt
currency=0
trade=0
converging_value=-1

amountOfActors=10000
amountOfResources=5

min_init_resources=0 
max_init_resources=100
min_init_production=-0.10
max_init_production=0.10

min_init_amountToSell=0
max_init_amountToSell=1
min_init_priceDivergence=-0.1 
max_init_priceDivergence=0.1
days=40
echo "Small resources" >> out.txt
amountOfResources=5
echo "Small population" >> out.txt
amountOfActors=10000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Medium population" >> out.txt
amountOfActors=50000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Large population" >> out.txt
amountOfActors=100000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Medium resources" >> out.txt
amountOfResources=10
echo "Small population" >> out.txt
amountOfActors=10000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Medium population" >> out.txt
amountOfActors=50000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Large population" >> out.txt
amountOfActors=100000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Large resources" >> out.txt
amountOfResources=20
echo "Small population" >> out.txt
amountOfActors=10000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Medium population" >> out.txt
amountOfActors=50000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run

echo "Large population" >> out.txt
amountOfActors=100000
echo "No-trade" >> out.txt
currency=0
trade=0
run

echo "Barter-trade" >> out.txt
currency=0
trade=1
run

echo "Gold-standard currency" >> out.txt
currency=1
trade=1
run