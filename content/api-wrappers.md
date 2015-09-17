Title: API wrappers: Danaïdes writing specifications
Date: 2015-09-15 14:00

API are awesome. They enable us to combine convenient applications with the expressive power of programming. They even create interactions between services not designed to work together.

When you want to use an API, you often have two possibilities: you can call the API yourself (with your favorite HTTP library), or you can use an API wrapper in your favorite language.

## API Wrappers are formal specifications in disguise

API wrappers are great, because they provide discoverability. You can use an API wrapper in your REPL or your IDE and just look at the objects and functions it provides to get an idea of what you can do with this API. Moreover, they provide a first layer of validation: if you use the API wrong, your IDE/compiler will tell you. API wrappers are a *formal and executable specifications* of the API.

However, the creation of that specification is problematic. It needs to be reverse-engineered from the API documentation (and often, by trial-and-error with the API itself), which can be a lot for work. For the wrapper to keep working, that specification need to be maintained up-to-date. And since that specification is encoded in an ad-hoc way in every wrapper library, that work is duplicated for every programming language (sometimes multiple times per programming language). This is a lot of wasted energy.

## How not to waste energy

Instead of all writing our own specifications for the same APIs, let's use a standard format to write it once, and collaborate to keep it up-to-date. [Swagger](http://swagger.io/), [RAML](http://raml.org/) and [API Blueprint](https://apiblueprint.org/) are good candidates for that job.

We'll then need a way to transform that specification into an actual API wrapper. We might use code generation or metaprogramming (and both approach are probably worth exploring). The formats I've mentioned already provide some tools to that effect, though I don't know to what extend.

Those specifications should be help up to the same standards as our code. We need ways to test automatically that they work and are still up to date.

Finally, we need the platform to bring all this together. More than just code sharing, it should provide a way to discover and understand existing specifications, and to easily find out if they are working and maintained. 

## The way forward

The closest I've seen to a solution is the [RAML APIs github group](https://github.com/raml-apis), which is a collection of popular APIs described in RAML, but it lacks information on how they are created, how up-to-date they are, and how to contribute.

Let's treat the API wrappers as the specifications they are, and collaborate between languages to share the work of creating them!
