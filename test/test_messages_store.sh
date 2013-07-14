echo "curl -X POST \
  -H \"Content-type: application/json\" \
  -d @test_messages_store.json \
  ${HOST}/messages/store"
curl -X POST \
  -H "Content-type: application/json" \
  -d @test_messages_store.json \
  ${HOST}/messages/store
