import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
  Chip,
  Pagination,
  Typography,
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import { DataGrid, useGridSlotComponentProps } from '@mui/x-data-grid';
import ProgressBar from '../Common/ProgressBar';
import moment from 'moment';

/* Temporary data */
const rows = [
  {
    id: 1,
    trueScore: 0.6,
    title: '9월 수출 558억 달러, 65년 무역 역사상 최고치…두 달 만에 기록 경신',
    date: new Date('2021-10-01'),
    emotionFilled: 0.2,
  },
  {
    id: 2,
    trueScore: 0.2,
    title: '“억지 부리지 말라”…野주자들, 이준석 때린 조수진 질타',
    date: new Date('2021-5-05'),
    emotionFilled: 0.8,
  },
  {
    id: 3,
    trueScore: 0.4,
    title: '급성 복통으로 출석 미룬 유동규…검찰, 응급실서 체포',
    date: new Date('2021-11-15'),
    emotionFilled: 0.55,
  },
];

const columns = [
  {
    field: 'trueScore',
    headerName: '팩트체크',
    width: 80,
    renderCell: (params) => (
      <div>
        {params.value >= 0.6 ? (
          <Chip color="success" label="진짜뉴스" />
        ) : (
          [
            params.value >= 0.4 ? (
              <Chip color="warning" label="의심뉴스" />
            ) : (
              <Chip color="error" label="가짜뉴스" />
            ),
          ]
        )}
      </div>
    ),
  },
  { field: 'title', headerName: '제목', flex: 1, minWidth: 150 },
  {
    field: 'date',
    headerName: '날짜',
    width: 100,
    renderCell: (params) => (
      <Typography>{moment(params.value).format('YYYY-MM-DD')}</Typography>
    ),
  },
  {
    field: 'emotionFilled',
    headerName: '감정수치',
    width: 100,
    renderCell: (params) => <ProgressBar value={Number(params.value)} />,
  },
];

const useStyles = makeStyles({
  root: {
    display: 'flex',
  },
});

function CustomPagination() {
  /* Custom Footer Pagination */
  const { state, apiRef } = useGridSlotComponentProps();
  const classes = useStyles();

  return (
    <Pagination
      className={classes.root}
      shape="rounded"
      count={state.pagination.pageCount}
      page={state.pagination.page + 1}
      onChange={(event, value) => apiRef.current.setPage(value - 1)}
    />
  );
}

export default function TrendsCard({ articles }) {
  return (
    <Card style={{ width: '100%', height: '400px' }}>
      <CardHeader title="트렌드" />
      <Divider />
      <CardContent>
        <Box sx={{ width: '100%', height: 300 }}>
          <DataGrid
            rows={rows}
            columns={columns}
            pagination
            pageSize={4}
            rowsPerPageOptions={[4]}
            components={{
              Pagination: CustomPagination,
            }}
          />
        </Box>
      </CardContent>
    </Card>
  );
}
