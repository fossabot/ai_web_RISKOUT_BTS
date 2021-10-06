import React from 'react';
import fileIcon from '../images/sub/file.png';
import ScrapButton from './ScrapButton';

export default function tableRow(props) {
  const {
    id,
    title,
    preview,
    author,
    href,
    showDetailModal,
    scrapArticle,
    isAlreadyScrapped,
  } = props;

  return (
    <tr>
      <td>
        <a href={href} title="외부링크">
          <img src={fileIcon} alt="filetype" />
        </a>
      </td>
      <td onClick={() => showDetailModal(id)} style={{ cursor: 'pointer' }}>
        <h3>{title}</h3>
        <p>{preview}</p>
      </td>
      <td>{author}</td>
      <td>
        <ScrapButton
          handleScrap={() => scrapArticle(id)}
          isAlreadyScrapped={isAlreadyScrapped}
        />
      </td>
    </tr>
  );
}
