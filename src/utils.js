export const extractDomain = (url) => {
    const domain = (new URL(url));
    return domain.hostname.replace('www.', '');
};
