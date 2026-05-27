export function extractApiData(response) {
  return response?.data?.data ?? response?.data
}

export function extractApiMessage(error, fallback = 'Something went wrong.') {
  return (
    error?.response?.data?.message ||
    error?.response?.data?.detail ||
    error?.message ||
    fallback
  )
}
