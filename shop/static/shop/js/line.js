import liff from '@line/liff';

document.addEventListener("DOMContentLoaded", () => {
    liff.init({liffId: "1657839732-YKbEZ0Oo"})
    .then(() => {
        if (!liff.isLoggedIn()) {
            liff.login({redirectUri: "192.168.0.14:8000"});
        }
    })
});