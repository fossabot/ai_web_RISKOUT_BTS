import client from '../client'

export async function getArticleVolume() {
  const response = await client.get('/api/article/volume')
  return response.data
}
