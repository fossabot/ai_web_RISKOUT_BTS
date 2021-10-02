import React from 'react';
import fileIcon from '../images/sub/file.png';

export default function tableRow(props) {
  const { id, title, preview, author, href, showDetailModal, scrapArticle } =
    props;

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
        <button onClick={() => scrapArticle(id)}>scrap</button>
      </td>
    </tr>
  );
}
