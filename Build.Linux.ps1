$tag = Get-Date -UFormat "%y%m%d%H"

Function BuildAndPushImage
{
	param([string]$Dockerfile, [string]$ImageName )

	docker build -t "${imageName}:${tag}" -f ./$Dockerfile .

	docker tag "${imageName}:${tag}" "${imageName}:latest"

	#docker push "${imageName}:${tag}"
	#docker push "${imageName}:${latestTag}"
}

BuildAndPushImage "Dockerfile.response.sql" "ashleypoole/monzo-response"
BuildAndPushImage "Dockerfile.cron" "ashleypoole/monzo-response-response-cron"