import client from '../client';

export async function getArticleVolume() {
  const response = await client.get('data/articleVolume.json');
  return response.data;
}
