import React from "react";

export default function filterCheckbox(props) {
    const { count, hashtag, onToggle } = props;
    const onChange = (e) => {
        onToggle(hashtag);
    }
    return (
        <li>
            <label>
                <input type="checkbox" onChange={onChange}/>
                <p>{hashtag}</p>
            </label>
            <em>{count > 10 ? '10+' : count}</em>
        </li>
    );
}
