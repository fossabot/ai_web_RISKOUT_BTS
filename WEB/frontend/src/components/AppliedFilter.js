import React from "react";
import closeIcon from "../images/sub/close_icon.png";

export default function appliedFilter(props) {
    const { hashtag, onRemoveHashtag } = props;

    return (
        <li>
            <p>{hashtag}</p>
            <button onClick={onRemoveHashtag}><img src={closeIcon} alt="" /></button>
        </li>
    )
}
