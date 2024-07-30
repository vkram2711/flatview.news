export const extractDomain = (url) => {
    const domain = (new URL(url));
    return domain.hostname.replace('www.', '');
};


// src/utils.js
export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}