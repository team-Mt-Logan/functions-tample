include .env

deploy:
	gcloud functions deploy sample_func \
	 --runtime python39 \
	 --trigger-topic=${TOPIC_ID} \
	 --memory=128MB \
	 --set-env-vars \
	 PROJECT_ID=${PROJECT_ID},DATASET=${DATASET},TABLE=${TABLE}
	 --timeout=60 
