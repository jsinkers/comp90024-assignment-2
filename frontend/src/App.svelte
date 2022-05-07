<script>
    import Tailwindcss from './Tailwindcss.svelte';
    import Sidebar from './Sidebar.svelte';
    import Map from './Map.svelte';
    import Landing from './Landing.svelte';
    import Landing2 from './Landing2.svelte';
    import Opportunity from './Opportunity.svelte';
    import SocialEngagement from './SocialEngagement.svelte';

    export let name;
    import {Router, Route, Link} from 'svelte-navigator';
    import DiversityScatter from "./DiversityScatter.svelte";
    import Line from "svelte-chartjs/src/Line.svelte"

</script>

<Tailwindcss />
<Router>
    <div>
        <header>
            <Sidebar />
        </header>

        <main>
            <div class="container">
                <Route>
                    <Landing2/>-->
                </Route>
                <Route path="opportunity/*">
                    <!-- TODO: page displays information about the indicator, data used - allow selection of visualisation -->
                    <!-- Alternatively - add info popup on the visualisations that provide this information -->
                    <Route path="/">
                        <Opportunity/>
                    </Route>
                    <Route path="/map">
                        <Map lat={-37.8136} lon={144.9631} zoom={9} />
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
                        <Map lat={-37.8136} lon={144.9631} zoom={9} />
                    </Route>
                    <Route path="/chart">
                        <!--TODO - election issues -->
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
    /*
    .container {
        @apply h-full w-11/12 absolute right-0 top-0 z-10;
    }
    */

    main {
        /*
        display: inline-block;
        */
    }

    header {
        display: inline-block;
    }

</style>
