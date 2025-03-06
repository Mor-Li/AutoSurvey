# run generation
python main.py --topic "LLMs for education" \
               --gpu 0,1,2,3 \
               --saving_path ./output/ \
               --model gpt-4o \
               --section_num 7 \
               --subsection_len 700 \
               --rag_num 60 \
               --outline_reference_num 1500 \
               --db_path ./database \
               --embedding_model nomic-ai/nomic-embed-text-v1 \
               --api_url http://152.69.226.145:3000/v1/chat/completions \
               --api_key sk-I6AFhSv1Qodu8FBx15126145600f4220A7D4Cc69Ef4810F7


# run evaluation
python evaluation.py --topic "LLMs for education" \
               --gpu 0,1,2,3 \
               --saving_path ./output/ \
               --model gpt-4o-2024-05-13 \
               --db_path ./database \
               --embedding_model nomic-ai/nomic-embed-text-v1 \
               --api_url http://152.69.226.145:3000/v1/chat/completions \
               --api_key sk-I6AFhSv1Qodu8FBx15126145600f4220A7D4Cc69Ef4810F7 
               
# unzip database
unzip database.zip -d ./database/
