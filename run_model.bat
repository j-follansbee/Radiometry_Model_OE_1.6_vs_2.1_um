python generate_CW_json.py
python generate_LRG_json.py

python run_CW_radiometry.py ./CW_input_jsons/*.json
python run_LRG_radiometry.py ./LRG_input_jsons/*.json

python parse_output_csvs.py ./CW_output_csvs/*.csv ./CW_combined_output.csv
python parse_output_csvs.py ./LRG_output_csvs/*.csv ./LRG_combined_output.csv

python terminate_at_unresolved.py ./CW_combined_output.csv ./CW_trimmed.csv
python terminate_at_unresolved.py ./LRG_combined_output.csv ./LRG_trimmed.csv