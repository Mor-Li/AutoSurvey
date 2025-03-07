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
               --model gpt-4o \
               --api_url http://152.69.226.145:3000/v1/chat/completions \
               --api_key sk-FQoAQv3CvhQEOPai4dBaBe7024C848D194F3B8110dE24eAf


# run evaluation
python evaluation.py --topic "LLMs for education" \
               --gpu 0,1,2,3 \
               --saving_path ./output/ \
               --model gpt-4o \
               --db_path ./database \
               --embedding_model nomic-ai/nomic-embed-text-v1 \
               --api_url http://152.69.226.145:3000/v1/chat/completions \
               --api_key sk-FQoAQv3CvhQEOPai4dBaBe7024C848D194F3B8110dE24eAf
               
# unzip database
unzip database.zip -d ./database/
