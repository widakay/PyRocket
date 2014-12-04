import boto, credentials, sys

# This is my second key for the PyRocket buckets
access_key = credentials.access_key
secret_key = credentials.secret_key


bucket_name = 'pyrocketprojects'
conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    host = 'objects.dreamhost.com',
)

bucket = conn.get_bucket(bucket_name)

print "Projects:"
for key in bucket.list(prefix='projects/project-'):
	print key.name

while True:
	projectId = raw_input("Please enter what project you would like to delete (CONTROL+C or return to cancel): ")
	if projectId == "":
		print "Cancelled... Goodbye!"
		sys.exit(0)

	print "\n\nWill delete:"
	print "----------------------------------------\n"
	delete_key_list = []
	for key in bucket.list(prefix='projects/project-' + str(projectId)):
		print key.name
		delete_key_list.append(key.name)

	print "\n----------------------------------------\n\n"


	if raw_input("Confirm? ").lower() == "y":
		print "Deleting..."
		if len(delete_key_list) > 0:
			bucket.delete_keys(delete_key_list)
		print "Done..."

	else:
		print "Cancelled"
	print "\n"