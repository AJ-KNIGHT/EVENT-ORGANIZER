function showSection(section) {
    let contentArea = document.getElementById('content-area');

    const bookingUrl = document.querySelector('[data-booking-url]')?.getAttribute('data-booking-url');
    const profileUpdateUrl = document.querySelector('[data-update-profile-url]')?.getAttribute('data-update-profile-url');
    const changeUrl = document.querySelector('[data-change-url]')?.getAttribute('data-change-url');
    const logoutUrl = document.querySelector('[data-logout-url]')?.getAttribute('data-logout-url');
    const adminUrl = document.querySelector('[data-admin-url]')?.getAttribute('data-admin-url');
    const changePasswordUrl = document.querySelector('[data-change-password-url]')?.getAttribute('data-change-password-url');

    if (section === 'events') {
        contentArea.innerHTML = `
            <h4>Event Management</h4>
            <p>Manage your events here.</p>
            <div class="d-grid gap-3">
                <a href="${bookingUrl}" class="btn btn-info w-100 custom-btn">Booking Dashboard</a>
                <a href="${changeUrl}" class="btn btn-warning w-100 custom-btn">Change Request Dashboard</a>
            </div>`;
    } else if (section === 'admin' && adminUrl) {
        contentArea.innerHTML = `
            <h4>Admin Dashboard</h4>
            <p>Welcome, Admin! Manage users, events, and requests here.</p>
            <div class="d-grid gap-3">
                <a href="${adminUrl}" class="btn btn-danger w-100 custom-btn">Admin Dashboard</a>
                <a href="${bookingUrl}" class="btn btn-info w-100 custom-btn">Booking Dashboard</a>
                <a href="${changeUrl}" class="btn btn-warning w-100 custom-btn">Change Request Dashboard</a>
            </div>`;
    } else {
        contentArea.innerHTML = `
            <h4>User Settings</h4>
            <p>Update your profile and change your password here.</p>
            <div class="d-grid gap-3">
                <a href="${profileUpdateUrl}" class="btn btn-primary w-100 custom-btn">Update Profile</a>
                <a href="${changePasswordUrl}" class="btn btn-warning w-100 custom-btn">Change Password</a>
                <a href="${logoutUrl}" class="btn btn-danger w-100 custom-btn">Logout</a>
            </div>`;
    }
}
