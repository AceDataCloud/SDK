# Retrieve an ACE Music task in Windmill

Create the resource type `ace_data_cloud` from `resource-type.json`. Store the token from your [Ace application](https://platform.acedata.cloud/console/applications) in a Windmill secret variable and reference the variable in the resource. Create a Python script from `get_task.py`. Select the saved resource and supply the ID of an existing task owned by the application.

The script queries the original task once. Use its group status to decide when to archive results. A partially failed group may still contain useful audio. Protect script run results that contain links to private audio. Repeating this lookup does not submit another song.
