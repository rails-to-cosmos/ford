(function(){const e=document.getElementById("navigation");Navbar=ReactBootstrap.Navbar,Button=ReactBootstrap.Button,Input=ReactBootstrap.Input;const t=React.createElement(Navbar,{bsStyle:"inverse"},React.createElement(Navbar.Header,null,React.createElement(Navbar.Toggle,null)),React.createElement(Navbar.Collapse,null,React.createElement(Navbar.Form,{pullLeft:!0},React.createElement(Input,{type:"text",placeholder:"Search"})," ",React.createElement(Button,{type:"submit"},"Submit")),React.createElement(Navbar.Form,{pullRight:!0},React.createElement(AuthorizationForm,null))));ReactDOM.render(t,e)}).call(this);
