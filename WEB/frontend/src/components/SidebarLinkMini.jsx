import Box from "@mui/material/Box";
import Link from "@mui/material/Link";

export default function SidebarLinkMini(props) {
    const { icon: ListIcon, text, href, isOn } = props;

    return (
        <Box className="iconMenuBox">
            <Link href={href} underline="none" className="inconMenuLink">
                <ListIcon sx={{ color: "#fff" }} className="iconMenu" />
            </Link>
        </Box>
    )
}
