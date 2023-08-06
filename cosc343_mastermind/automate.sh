#!/bin/bash
for sample in 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
do
  for lower_bound in 300 400 500 600 700 800 900
  do
    python update_settings.py --sample $sample --lower_bound $lower_bound
    echo "Sample: $sample, Lower bound: $lower_bound" >> tests
    python mastermind.py >> tests
  done
done