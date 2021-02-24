import React from "react"
import { connect } from "react-redux"
import { Route, Link } from "react-router-dom";
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import Hidden from '@material-ui/core/Hidden';
import IconButton from '@material-ui/core/IconButton';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import MailIcon from '@material-ui/icons/Mail';
import MenuIcon from '@material-ui/icons/Menu';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles, useTheme } from '@material-ui/core/styles';


const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: drawerWidth,
      flexShrink: 0,
    },
  },
  appBar: {
    [theme.breakpoints.up('sm')]: {
      width: `calc(100% - ${drawerWidth}px)`,
      marginLeft: drawerWidth,
    },
  },
  menuButton: {
    marginRight: theme.spacing(2),
    [theme.breakpoints.up('sm')]: {
      display: 'none',
    },
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: drawerWidth
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

const mapStateToProps = state => {
  return {}
}
const mapDispatchToProps = {}
const PublicTemplate = connect(
  mapStateToProps,
  mapDispatchToProps
)(props => {

  const { window } = props;
  const classes = useStyles();
  const theme = useTheme();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <div className={classes.toolbar}  >
        <h1 style={{ textAlign: "center", paddingTop: "5%" }}>
          iFASTATHANU
      </h1>
      </div>

      <Divider />
      <List>
        <Link style={{ textDecoration: 'none' }}  to="/main">
          <ListItem button key="MainBoard">
            <ListItemIcon><InboxIcon /></ListItemIcon>
            <ListItemText primary={"MainBoard"} />
          </ListItem>
        </Link>

        <Link style={{ textDecoration: 'none' }} to="/live">
          <ListItem button key="Live">
            <ListItemIcon><InboxIcon /></ListItemIcon>
            <ListItemText primary={"Live"} />
          </ListItem>
        </Link>

        <Link style={{ textDecoration: 'none' }} to="/history">
          <ListItem button key="History">
            <ListItemIcon><InboxIcon /></ListItemIcon>
            <ListItemText primary={"History"} />
          </ListItem>
        </Link>

        <Link style={{ textDecoration: 'none' }} to="/about">
          <ListItem button key="About">
            <ListItemIcon><InboxIcon /></ListItemIcon>
            <ListItemText primary={"About"} />
          </ListItem>
        </Link>
      </List>
      <Divider />

    </div>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            className={classes.menuButton}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap>
            iFASTATHANU
          </Typography>
        </Toolbar>
      </AppBar>
      <nav className={classes.drawer} aria-label="mailbox folders">
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Hidden smUp implementation="css">
          <Drawer
            container={container}
            variant="temporary"
            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
            open={mobileOpen}
            onClose={handleDrawerToggle}
            classes={{
              paper: classes.drawerPaper,
            }}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
          >
            {drawer}
          </Drawer>
        </Hidden>
        <Hidden xsDown implementation="css">
          <Drawer
            classes={{
              paper: classes.drawerPaper,
            }}
            variant="permanent"
            open
          >
            {drawer}
          </Drawer>
        </Hidden>
      </nav>

      <main className={classes.content}>
        <div className={classes.toolbar} />
        {props.children}
      </main>
    </div>

  )
})

const PublicTemplateRoute = ({ component: Component, ...rest }) => {
  return (

    <Route
      {...rest}
      render={matchProps => (
        <PublicTemplate>
          <Component {...matchProps} />
        </PublicTemplate>
      )}
    />
  )
}

export default PublicTemplateRoute;