const UserInfo = ({ user }) => (
  <section className="user-info">
    {user ? (
      <>
        <h2>Hello, {user.username}!</h2>
        <p>Email: {user.email}</p>
      </>
    ) : (
      <p>Loading user data...</p>
    )}
  </section>
);

export default UserInfo;