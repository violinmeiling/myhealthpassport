import { createRoot } from 'react-dom/client';
import { withAuthInfo } from '@propelauth/react';

function NavigationBar() {
  // TODO: Actually implement a navigation bar
  const YourApp = withAuthInfo((props) => {
    // isLoggedIn and user are injected automatically from withAuthInfo
    if (props.isLoggedIn) {
        return <p>You are logged in as {props.user.email}</p>
    } else {
        return <p>You are not logged in</p>
    }
})
}

const domNode = document.getElementById('navigation');
const root = createRoot(domNode);
root.render(<NavigationBar />);