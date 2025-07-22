# create-helm

create helm chart from helm  release secret 

kubectl  get secret sh.helm.release.v1.x -o go-template='{{.data.release | base64decode | base64decode}}' | gzip -d | jq > data.json
