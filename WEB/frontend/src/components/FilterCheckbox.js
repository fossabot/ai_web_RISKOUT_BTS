import React from "react";

export default function filterCheckbox(props) {
    const { count, hashtag, isChecked, onToggle } = props;
    const onChange = (e) => {
        onToggle(hashtag);
    }
    return (
        <li>
            <label>
                <input type="checkbox" onChange={onChange} defaultChecked={isChecked}/>
                <p>{hashtag}</p>
            </label>
            <em>{count > 10 ? '10+' : count}</em>
        </li>
    );
}
