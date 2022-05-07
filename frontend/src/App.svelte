<script>
    import Tailwindcss from './Tailwindcss.svelte';
    import Sidebar from './Sidebar.svelte';
    import Map from './Map.svelte';
    import Landing from './Landing.svelte';

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
                    <!--TODO: Default route - landing page-->
                    <!--<Landing/>-->
                    Exploring livability in Melbourne through the Australian Federal election 2022
                </Route>
                <Route path="opportunity/*">
                    <!-- TODO: page displays information about the indicator, data used - allow selection of visualisation -->
                    <!-- Alternatively - add info popup on the visualisations that provide this information -->
                    <!--<h1>Opportunity</h1>-->
                    <Route path="/map">
                        <Map lat={-37.8136} lon={144.9631} zoom={9} />
                    </Route>
                    <Route path="/chart">
                        <DiversityScatter/>
                    </Route>
                </Route>
                <Route path="social-engagement/*">
                    <h1>Opportunity</h1>
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

                </Route>
            </div>
        </main>
    </div>
</Router>

<style>
    .container {
        height: 100%;
    }

    main {
        height:100%;
        /*
        display: inline-block;
        */
    }

    header {
        display: inline-block;
    }

</style>
