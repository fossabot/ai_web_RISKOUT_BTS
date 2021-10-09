import {
  IconButton,
  Link,
  Typography,
  TableCell,
  TableRow,
} from '@mui/material';
import AddBoxIcon from '@mui/icons-material/AddBox';
import DescriptionIcon from '@mui/icons-material/Description';

export default function SecretsTableRow(props) {
  const { id, title, preview, author, href, showDetailModal } = props;

  return (
    <TableRow
      key={id}
      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
    >
      <TableCell component="th" scope="row">
        <Link href={href} underline="hover">
          <DescriptionIcon />
        </Link>
      </TableCell>
      <TableCell
        align="left"
        onClick={() => showDetailModal(id)}
        style={{ cursor: 'pointer' }}
      >
        <Typography style={{ fontWeight: 'bold' }} color="textPrimary">
          {title}
        </Typography>
        <Typography color="textSecondary" variant="body2">
          {preview}
        </Typography>
      </TableCell>
      <TableCell align="center">{author}</TableCell>
      <TableCell align="center">
        <IconButton>
          <AddBoxIcon />
        </IconButton>
      </TableCell>
    </TableRow>
  );
}
