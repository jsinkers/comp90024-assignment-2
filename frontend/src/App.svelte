<script>
    import {Router, Route, Link} from 'svelte-navigator';
    import Tailwindcss from './Tailwindcss.svelte';
    import Sidebar from './Sidebar.svelte';

    import Landing2 from './Landing2.svelte';
    import Opportunity from './Opportunity.svelte';
    import SocialEngagement from './SocialEngagement.svelte';
    import DiversityMap from './DiversityMap.svelte';
    import DiversityScatter from "./DiversityScatter.svelte";
    import SeifaMap from './SeifaMap.svelte';
    import SeifaChart from './SeifaChart.svelte';

    export let name;
</script>

<Tailwindcss />
<Router>
    <div>
        <header>
            <Sidebar />
        </header>

        <main>
            <div class="body-container">
                <Route>
                    <Landing2/>
                </Route>
                <Route path="opportunity/*">
                    <!-- TODO: page displays information about the indicator, data used - allow selection of visualisation -->
                    <!-- Alternatively - add info popup on the visualisations that provide this information -->
                    <Route path="/">
                        <Opportunity/>
                    </Route>
                    <Route path="/map">
                        <DiversityMap lat={-37.8136} lon={144.9631} zoom={9} />
                    </Route>
                    <Route path="/chart">
                        <DiversityScatter/>
                    </Route>
                </Route>
                <Route path="social-engagement/*">
                    <Route path="/">
                        <SocialEngagement/>
                    </Route>
                    <Route path="/map">
                        <!-- TODO: create different map/parametrise existing component -->
                        <SeifaMap lat={-37.8136} lon={144.9631} zoom={9} />
                    </Route>
                    <Route path="/chart">
                        <!--TODO - election issues -->
                        <SeifaChart/>
                    </Route>
                </Route>
                <Route path="about">
                    <!--TODO -->
                    Developed for COMP90024 by
                    <ul>
                        <li></li>
                    </ul>
                </Route>
            </div>
        </main>
    </div>
</Router>

<style>
    header {
        display: inline-block;
    }

    .body-container {
        @apply h-full w-11/12 absolute right-0 top-0 z-10;
        display: flex;
        justify-content: center;
    }
</style>
