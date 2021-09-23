import React from "react";

export default function filterCheckbox(props) {
    const { count, hashtag } = props;
    return (
        <li>
            <label>
                <input type="checkbox" />
                <p>{hashtag}</p>
            </label>
            <em>{count > 10 ? '10+' : count}</em>
        </li>
    );
}