import Link from "@mui/material/Link";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";

export default function SidebarLink(props) {

    const { icon: ListIcon, text, href, isOn } = props;

    // <SidebarLink icon={SearchIcon} text="탐지현황" href="/detectionstatus" isOn={true} />

    return (
        <ListItem className="pin">
            <Link href={href} underline="none" className="list">
                <ListItemButton className={isOn && "on"}>
                    <ListIcon className="icon" />
                    <ListItemText primary={text} className="link" />
                </ListItemButton>
            </Link>
        </ListItem>
    )
}