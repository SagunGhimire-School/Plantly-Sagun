import { currentUser } from '../../lib/session';
import Logout from '../../features/logout';
import Garden from '../../features/garden';
import Workspace from '../../features/workspace';

export default async function Dashboard({searchParams}) {
  const user = await currentUser();
  const params = await searchParams;
  if (!user) return <section><h1>Your garden is temporarily unavailable.</h1><p>The local backend could not be reached. Try refreshing shortly.</p></section>;
  return <Workspace><section className="narrow"><p className="eyebrow">YOUR GARDEN</p><h1>Your season starts here.</h1><p>Signed in as {user.email}.</p><Logout /><Garden plotId={params.plot_id} seasonId={params.season_id}/></section></Workspace>;
}
