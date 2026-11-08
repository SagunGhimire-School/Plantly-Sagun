import { currentUser } from '../../lib/session';
import Onboarding from '../../features/onboarding';
import Workspace from '../../features/workspace';

export default async function OnboardingPage() {
  const user = await currentUser();
  if (!user) return <section><h1>Your draft is temporarily unavailable.</h1><p>Try refreshing when the local backend is running.</p></section>;
  return <Workspace><Onboarding /></Workspace>;
}
