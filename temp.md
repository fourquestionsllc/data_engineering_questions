g.V().
  has("node_type", "Project").
  has("id", projectId).
  bothE().
  otherV().
  has("node_type", "ProjectApproval").
  limit(1).
  hasNext()
