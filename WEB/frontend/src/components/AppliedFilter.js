// import React from "react";
import closeIcon from '../images/sub/close_icon.png';
import Chip from '@mui/material/Chip';

export default function appliedFilter(props) {
  const { hashtag, onRemoveHashtag } = props;
  const handleDelete = () => {
    onRemoveHashtag(hashtag);
  };

  return (
    // <Chip label={hashtag} variant="outlined" onDelete={handleDelete} />
    <li>
      <p>{hashtag}</p>
      <button onClick={handleDelete}>
        <img src={closeIcon} alt="" />
      </button>
    </li>
  );
}
